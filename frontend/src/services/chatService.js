
import api from "./api";

export const sendChatMessage = async ({
  astronautId = null,
  conversationId = null,
  message,
}) => {
  const response = await api.post(
    "/chat",
    {
      astronaut_id: astronautId,
      conversation_id: conversationId,
      message,
    },
    {
      // The AI service may take longer than the default 10 seconds.
      timeout: 60000,
    }
  );

  return response.data;
};
