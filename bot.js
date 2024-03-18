const { OpenAI } = require('openai');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());
app.use(cors());

const apiKey = process.env.API_KEY

const openai = new OpenAI({ apiKey: apiKey });

app.get('/', (req, res) => {
    res.send('Welcome!!');
});

app.post('/message', async (req, res) => {
    try {
        const response = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: [{ role: 'system', content: 'You are a helpful assistant.' }, { role: 'user', content: req.body.message }],
        });

        const botMessage = response.choices[0].message.content;
        const message = { message: botMessage };

        res.send(message);
    } catch (err) {
        console.error('Error fetching response from OpenAI API:', err);
        res.status(500).send({ error: 'Internal Server Error' });
    }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Listening on port ${PORT}`));