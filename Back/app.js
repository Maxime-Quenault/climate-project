const express = require('express');
const app = express();

const port = 3000;

// Route pour la page d'accueil
app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// Démarrer le serveur
app.listen(port, () => {
    console.log(`Serveur démarré sur http://localhost:${port}`);
});