// importar librerias
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const { ApolloServer, gql } = require('apollo-server-express');

// importar modelos
const Usuario = require('./models/usuario');

// conexion a la base de datos mongodb
mongoose.connect('mongodb://localhost:27017/dwm2');


// definicion del esquema
const typeDefs  = gql`
    type Usuario {
        id: ID
        nombre: String
        pass: String
    }
    input UsuarioInput {
        nombre: String!
        pass: String!
    }
        
    type response {
        status: String
        message: String
    }

    type Query {
        getUsuarios: [Usuario]
        getUsuarioById(id: ID!): Usuario
    }

    type Mutation {
        addUsuario(input: UsuarioInput): Usuario
        updateUsuario(id: ID!, input: UsuarioInput): Usuario
        deleteUsuario(id: ID!): response
    }
`;

const resolvers = {
    // para leer de la base de datos (consulta)
    Query:{
        async getUsuarios(obj) {
            const usuarios = await Usuario.find();
            return usuarios;
        },
        async getUsuarioById(obj, { id }) {
            const usuarioBus = await Usuario.findById(id);
            if(usuarioBus == null){
                return null;
            }else{
                return usuarioBus;
            }
        }
    },
    // para escribir en la base de datos
    Mutation: {
        async addUsuario(obj, { input }) {
            const usuario = new Usuario(input);
            await usuario.save();
            return usuario;
        },

        async updateUsuario(obj, { id, input }) {
            const usuario = await Usuario.findByIdAndUpdate(id, input);
            return usuario;
        },

        async deleteUsuario(obj, { id }) {
            await Usuario.deleteOne({ _id: id });
            return{
                status: "200",
                message: "Usuario eliminado"
            }
        }
    }
}

let apolloServer = null;

const corsoptions = {
    origin: 'http://localhost:8090',
    credentials : false
};


async function startServer() {
    apolloServer = new ApolloServer({typeDefs, resolvers, corsoptions});
    await apolloServer.start();
    apolloServer.applyMiddleware({app, cors: false});
}


startServer();
const app = express();
app.use(cors());
app.listen(8090, function() {
    console.log('Servidor iniciado en el puerto 8090');
});