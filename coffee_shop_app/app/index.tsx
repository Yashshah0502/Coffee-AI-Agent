/// <reference types="nativewind/types" />
import { Text, View, ImageBackground, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { router } from "expo-router";

export default function Index() {
  return (
    <SafeAreaView className="flex-1">
      <ImageBackground
        className="w-full h-full items-center justify-end pb-20"
        source={require("../assets/Images/index_bg_image.png")}
        resizeMode="cover"
      >
        <View className="w-[80%]">
          <Text className="text-white text-3xl text-center font-[Sora-SemiBold]">
            Fall in Love with Coffee in Blissful Delight!
          </Text>

          <Text className="pt-3 text-[#A2A2A2] text-center font-[Sora-Regular]">
            Welcome to our cozy coffee corner, where every cup is a delightful
            for you.
          </Text>

          <TouchableOpacity
            className="bg-[ #C57C3E] mt-10 p-3 rounded-lg items-center"
            onPress={() => router.push("/(tabs)/home")}
          >
            <Text className="text-xl text-white font-[Sora-SemiBold]">
              Get Started
            </Text>
          </TouchableOpacity>
        </View>
      </ImageBackground>
    </SafeAreaView>
  );
}
