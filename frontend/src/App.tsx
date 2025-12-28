import { useChat } from "@ai-sdk/react"
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation"
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message"
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputSubmit,
} from "@/components/ai-elements/prompt-input"
import { Card } from "@/components/ui/card"
import { MessageCircle } from "lucide-react"

function App() {
  const { messages, handleSubmit, status, input, setInput } = useChat({
    api: "/api/chat",
  })

  const isLoading = status === "streaming" || status === "submitted"

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="flex flex-col h-[600px] w-full max-w-2xl">
        <div className="p-4 border-b">
          <h2 className="text-lg font-semibold">Chat</h2>
        </div>

        <Conversation className="flex-1">
          <ConversationContent>
            {messages.length === 0 ? (
              <ConversationEmptyState
                title="Start a conversation"
                description="Send a message to begin chatting with the AI assistant"
                icon={<MessageCircle className="size-8" />}
              />
            ) : (
              messages.map((message) => (
                <Message key={message.id} from={message.role}>
                  <MessageContent>
                    {message.role === "assistant" ? (
                      <MessageResponse>{message.content}</MessageResponse>
                    ) : (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    )}
                  </MessageContent>
                </Message>
              ))
            )}
            {isLoading && messages[messages.length - 1]?.role === "user" && (
              <Message from="assistant">
                <MessageContent>
                  <p className="text-muted-foreground">Thinking...</p>
                </MessageContent>
              </Message>
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        <div className="p-4 border-t">
          <PromptInput
            onSubmit={({ text }, event) => {
              handleSubmit(event, { data: { message: text } })
            }}
          >
            <PromptInputTextarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              disabled={isLoading}
            />
            <PromptInputFooter>
              <div />
              <PromptInputSubmit status={status} disabled={isLoading} />
            </PromptInputFooter>
          </PromptInput>
        </div>
      </Card>
    </div>
  )
}

export default App
