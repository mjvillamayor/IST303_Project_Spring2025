const express = require('express');
const db = require('./database');

const app = express();
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Medication Management System API is running');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log('Server running on port ${PORT}'));
