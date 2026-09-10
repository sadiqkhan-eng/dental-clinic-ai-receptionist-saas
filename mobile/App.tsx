import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { ClerkProvider, SignedIn, SignedOut } from "@clerk/clerk-expo";
import { View, Text, TouchableOpacity } from "react-native";

const Stack = createStackNavigator();

function HomeScreen() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center", padding: 20 }}>
      <Text style={{ fontSize: 28, fontWeight: "bold", color: "#2563eb" }}>DentalOS</Text>
      <Text style={{ fontSize: 16, color: "#666", marginTop: 8 }}>AI-Powered Dental Clinic</Text>
    </View>
  );
}

function SignInScreen() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Sign In</Text>
    </View>
  );
}

export default function App() {
  return (
    <ClerkProvider publishableKey="pk_test_xxx">
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="Home" component={HomeScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </ClerkProvider>
  );
}
