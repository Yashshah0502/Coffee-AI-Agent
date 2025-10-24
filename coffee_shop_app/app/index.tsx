import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { StatusBar } from "expo-status-bar";

export default function Index() {
  return (
    <View className="flex-1 bg-amber-50">
      <StatusBar style="dark" />
      
      {/* Header */}
      <View className="bg-amber-800 pt-12 pb-6 px-6">
        <Text className="text-3xl font-bold text-white mb-2">
          ☕ Coffee Shop AI
        </Text>
        <Text className="text-amber-100 text-base">
          Your intelligent coffee ordering assistant
        </Text>
      </View>

      <ScrollView className="flex-1">
        {/* Welcome Section */}
        <View className="p-6">
          <Text className="text-2xl font-bold text-amber-900 mb-3">
            Welcome!
          </Text>
          <Text className="text-base text-gray-700 leading-6 mb-4">
            Our AI-powered chatbot is here to help you discover the perfect 
            coffee, take your order, and provide personalized recommendations 
            based on your preferences.
          </Text>
        </View>

        {/* Features Grid */}
        <View className="px-6 pb-6">
          <Text className="text-xl font-bold text-amber-900 mb-4">
            Features
          </Text>
          
          <View className="space-y-4">
            {/* Feature Card 1 */}
            <View className="bg-white rounded-xl p-5 shadow-sm border border-amber-200">
              <Text className="text-lg font-semibold text-amber-800 mb-2">
                🤖 Smart Assistant
              </Text>
              <Text className="text-gray-600 leading-5">
                Ask questions about our menu, hours, and location. Get instant answers!
              </Text>
            </View>

            {/* Feature Card 2 */}
            <View className="bg-white rounded-xl p-5 shadow-sm border border-amber-200 mt-4">
              <Text className="text-lg font-semibold text-amber-800 mb-2">
                🛒 Easy Ordering
              </Text>
              <Text className="text-gray-600 leading-5">
                Place orders naturally through conversation. Our AI understands you.
              </Text>
            </View>

            {/* Feature Card 3 */}
            <View className="bg-white rounded-xl p-5 shadow-sm border border-amber-200 mt-4">
              <Text className="text-lg font-semibold text-amber-800 mb-2">
                ⭐ Personalized Recommendations
              </Text>
              <Text className="text-gray-600 leading-5">
                Get smart suggestions based on popular items and what pairs well together.
              </Text>
            </View>
          </View>
        </View>

        {/* CTA Button */}
        <View className="px-6 pb-8">
          <TouchableOpacity 
            className="bg-amber-700 rounded-full py-4 px-8 shadow-lg active:bg-amber-800"
            activeOpacity={0.8}
          >
            <Text className="text-white text-center text-lg font-bold">
              Start Chatting
            </Text>
          </TouchableOpacity>
        </View>

        {/* Tech Info */}
        <View className="bg-amber-100 mx-6 mb-8 rounded-lg p-4 border border-amber-300">
          <Text className="text-sm font-semibold text-amber-900 mb-2">
            Powered by Advanced AI
          </Text>
          <Text className="text-xs text-amber-800 leading-5">
            Using Meta Llama 3.1 8B, RAG with Pinecone vector database, 
            and Apriori algorithm for market basket analysis.
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}
