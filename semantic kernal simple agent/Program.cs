using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using System.ComponentModel;


var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "<YOUR_DEPLOYMENT_NAME>",
    endpoint: "<YOUR_ENDPOINT>",
    apiKey: "<YOUR_AZURE_OPENAI_API_KEY>"
);
builder.Plugins.AddFromType<TimeTeller>(); // <------------ Telling kernel about time plugins



var kernel = builder.Build();
IChatCompletionService chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

ChatHistory chatMessages = new ChatHistory("""
You are a friendly assistant who likes to follow the rules. You will complete required steps
and request approval before taking any consequential actions. If the user doesn't provide
enough information for you to complete a task, you will keep asking questions until you have
enough information to complete the task.
""");

Console.WriteLine("Assistant > How may I help you?");





while (true)
{
    Console.Write("User > ");
    chatMessages.AddUserMessage(Console.ReadLine()!);
    OpenAIPromptExecutionSettings settings = new() { ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions };
    var result = chatCompletionService.GetStreamingChatMessageContentsAsync(
        chatMessages,
        executionSettings: settings,
        kernel: kernel);

    Console.Write("Assistant > ");
    // Stream the results
    string fullMessage = "";
    await foreach (var content in result)
    {
        Console.Write(content.Content);
        fullMessage += content.Content;
    }
    Console.WriteLine("\n--------------------------------------------------------------");

    // Add the message from the agent to the chat history
    chatMessages.AddAssistantMessage(fullMessage);
}



public class TimeTeller // <------------ Time teller plugin. An expert on time, peak and off-peak periods
{
    [Description("This function retrieves the current time.")]
    [KernelFunction]
    public string GetCurrentTime() => DateTime.Now.ToString("F");

    [Description("This function checks if in off-peak period between 9pm and 7am")]
    [KernelFunction]
    public bool IsOffPeak() => DateTime.Now.Hour < 7 || DateTime.Now.Hour >= 21;
}
