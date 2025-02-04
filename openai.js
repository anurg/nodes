import OpenAI from 'openai'
import dotenv from 'dotenv'

// Initialize dotenv
dotenv.config();

const openai = new OpenAI(
    {
        apiKey:process.env.OPENAI_API_KEY,
        dangerouslyAllowBrowser:true
    }
)
const messages = [
    {
        role:'system',
        content:'You are a Quantum Computer Expert.Explain the asked question about quantum computing like different agen groups as asked by the user.'
    },
    {
        role:'user',
        content:'Explain Quantum computing to high School student.'
    }
]
const response = await openai.chat.completions.create({
    model:'gpt-4',
    messages:messages
})
console.log(response.choices[0].message.content)