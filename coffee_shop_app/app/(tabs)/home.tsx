/// <reference types="nativewind/types" />
import { View, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function Home() {
  return (
    <SafeAreaView className="flex-1 bg-black">
      <View className="flex-1 items-center justify-center">
        <Text className="text-white text-3xl font-[Sora-Bold]">
          Coffee Shop Home
        </Text>
        <Text className="text-gray-400 text-base mt-4 font-[Sora-Regular]">
          Welcome to your coffee shop!
        </Text>
      </View>
    </SafeAreaView>
  );
}
