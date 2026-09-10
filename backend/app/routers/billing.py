import asyncio
from fastapi import APIRouter, Request, HTTPException
import stripe

from app.config import settings

router = APIRouter()

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/checkout")
async def create_checkout_session(clinic_id: str, plan: str):
    price_map = {
        "solo": "price_solo_monthly",
        "growth": "price_growth_monthly",
        "clinic_group": "price_clinic_group_monthly",
    }

    session = await asyncio.to_thread(
        stripe.checkout.Session.create,
        mode="subscription",
        line_items=[{"price": price_map.get(plan, price_map["solo"]), "quantity": 1}],
        success_url="http://localhost:3000/dashboard/billing?success=true",
        cancel_url="http://localhost:3000/dashboard/billing?canceled=true",
        metadata={"clinic_id": clinic_id, "plan": plan},
    )

    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = await asyncio.to_thread(
            stripe.Webhook.construct_event,
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        clinic_id = session["metadata"]["clinic_id"]
        plan = session["metadata"]["plan"]
        stripe_customer_id = session["customer"]
        stripe_subscription_id = session["subscription"]

        from sqlalchemy import select
        from app.database import async_session
        from app.models import Subscription

        async with async_session() as db:
            result = await db.execute(
                select(Subscription).where(Subscription.clinic_id == clinic_id)
            )
            sub = result.scalar_one_or_none()
            if sub:
                sub.stripe_customer_id = stripe_customer_id
                sub.stripe_subscription_id = stripe_subscription_id
                sub.plan = plan
                sub.status = "active"
            else:
                sub = Subscription(
                    clinic_id=clinic_id,
                    stripe_customer_id=stripe_customer_id,
                    stripe_subscription_id=stripe_subscription_id,
                    plan=plan,
                    status="active",
                )
                db.add(sub)
            await db.commit()

    return {"status": "ok"}
