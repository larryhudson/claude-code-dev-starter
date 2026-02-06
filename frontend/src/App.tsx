import { useChat } from "@ai-sdk/react"
import { useState } from "react"
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
import { MessageCircle, Wrench, CheckCircle, Loader2 } from "lucide-react"

// Helper to check if a part is a tool part
function isToolPart(part: { type: string }): part is ToolPart {
  return part.type.startsWith("tool-") || part.type === "dynamic-tool"
}

// Type for tool parts
interface ToolPart {
  type: string
  toolCallId: string
  toolName?: string // for dynamic-tool
  state: "input-streaming" | "input-available" | "result" | "error"
  input?: unknown
  output?: unknown
  errorText?: string
}

// Component to render a tool call
function ToolCall({ part }: { part: ToolPart }) {
  // Extract tool name from type (e.g., "tool-get_project_info" -> "get_project_info")
  const toolName = part.type === "dynamic-tool"
    ? part.toolName
    : part.type.replace("tool-", "")

  const isComplete = part.state === "result"
  const isError = part.state === "error"
  const isLoading = part.state === "input-streaming" || part.state === "input-available"

  return (
    <div className={`my-2 rounded-lg border p-3 text-sm transition-colors ${
      isComplete ? 'bg-primary/5 border-primary/20' :
      isError ? 'bg-destructive/5 border-destructive/20' :
      'bg-muted/50 border-border'
    }`}>
      <div className="flex items-center gap-2 font-medium">
        {isLoading && <Loader2 className="size-4 animate-spin text-primary" />}
        {isComplete && <CheckCircle className="size-4 text-primary" />}
        {isError && <span className="size-4 text-destructive font-bold">!</span>}
        <Wrench className={`size-4 ${isComplete ? 'text-primary' : ''}`} />
        <span>{toolName}</span>
      </div>
      {part.input && (
        <details className="mt-2">
          <summary className="cursor-pointer text-xs text-muted-foreground hover:text-foreground transition-colors">Input</summary>
          <pre className="mt-1 overflow-auto rounded bg-background p-2 text-xs border border-border/50">
            {JSON.stringify(part.input, null, 2)}
          </pre>
        </details>
      )}
      {part.output && (
        <details className="mt-2" open>
          <summary className="cursor-pointer text-xs text-muted-foreground hover:text-foreground transition-colors">Output</summary>
          <pre className="mt-1 overflow-auto rounded bg-background p-2 text-xs border border-border/50">
            {JSON.stringify(part.output, null, 2)}
          </pre>
        </details>
      )}
      {part.errorText && (
        <div className="mt-2 text-xs text-destructive">{part.errorText}</div>
      )}
    </div>
  )
}

function App() {
  const { messages, sendMessage, status } = useChat({
    api: "/api/chat",
  })
  const [input, setInput] = useState("")

  const isLoading = status === "streaming" || status === "submitted"

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary/5 to-background flex items-center justify-center p-4">
      <Card className="flex flex-col h-[600px] w-full max-w-2xl shadow-xl border-border/50 rounded-2xl overflow-hidden">
        <div className="px-5 py-4 border-b bg-card">
          <h2 className="text-lg font-semibold text-primary flex items-center gap-2">
            <MessageCircle className="size-5" />
            Chat
          </h2>
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
              messages.map((message) => {
                return (
                  <Message key={message.id} from={message.role}>
                    <MessageContent>
                      {message.parts.map((part, index) => {
                        // Render text parts
                        if (part.type === "text") {
                          const textPart = part as { type: "text"; text: string }
                          return message.role === "assistant" ? (
                            <MessageResponse key={index}>{textPart.text}</MessageResponse>
                          ) : (
                            <p key={index} className="whitespace-pre-wrap">{textPart.text}</p>
                          )
                        }

                        // Render tool parts
                        if (isToolPart(part)) {
                          return <ToolCall key={index} part={part as ToolPart} />
                        }

                        return null
                      })}
                    </MessageContent>
                  </Message>
                )
              })
            )}
            {isLoading && messages[messages.length - 1]?.role === "user" && (
              <Message from="assistant">
                <MessageContent>
                  <div className="flex items-center gap-2 text-primary">
                    <Loader2 className="size-4 animate-spin" />
                    <span>Thinking...</span>
                  </div>
                </MessageContent>
              </Message>
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        <div className="p-4 border-t bg-card">
          <PromptInput
            onSubmit={({ text }) => {
              if (text.trim()) {
                void sendMessage({ text })
                setInput("")
              }
            }}
          >
            <PromptInputTextarea
              value={input}
              onChange={(e) => { setInput(e.target.value); }}
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
