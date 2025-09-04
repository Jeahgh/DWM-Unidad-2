// como se va a llamar el modelo en la base de datos
// y que campos va a tener


const mongoose = require('mongoose');
// Importa Mongoose, el traductor entre JS y MongoDB.

const usuarioSchema = mongoose.Schema({
    nombre: String,
    pass: String
});

// Define la "forma" (schema) de un documento Usuario en MongoDB.
// Dos campos: nombre y pass. Por defecto Mongo agrega _id.

module.exports = mongoose.model('Usuario', usuarioSchema);
// Crea el MODELO 'Usuario' (colección 'usuarios') y lo exporta.
// Ahora puedes hacer Usuario.find(), Usuario.findById(), new Usuario(), etc.