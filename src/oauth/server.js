const express = require('express')
const session = require('express-session')
const crypto = require('crypto')
const fetch = require('node-fetch')
const {exec} = require('child_process')

const app = express()
const port = 3000
const clientId = 'Testing'

app.use(session({ resave: true, secret: 'SECRET', saveUninitialized: true }))

app.get('/', (req, res) => {
    res.send('<a href="/login">Login</a>')
})

const base64URLEncode = (str) => {
    return str.toString('base64')
    	.replace(/\+/g, '-')
    	.replace(/\//g, '_')
    	.replace(/=/g, '')
}

const sha256 = (buffer) => crypto.createHash('sha256').update(buffer).digest()
const createVerifier = () => base64URLEncode(crypto.randomBytes(32))
const createChallenge = (verifier) => base64URLEncode(sha256(verifier))

app.get('/login', async (req, res) => {
    const url = req.protocol + '://' + req.get('host') + req.baseUrl
    const verifier = createVerifier()
    const challenge = createChallenge(verifier)
    req.session.codeVerifier = verifier
    res.redirect('https://lichess.org/oauth?' + new URLSearchParams({
        response_type: 'code',
    	client_id: clientId,
    	redirect_uri: `${url}/oauth_token`,
    	scope: 'preference:read challenge:read bot:play board:play',
    	code_challenge_method: 'S256',
    	code_challenge: challenge
    }))
})

const getLichessToken = async (authCode, verifier, url) => await fetch('https://lichess.org/api/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
	grant_type: 'authorization_code',
	redirect_uri: `${url}/oauth_token`,
        client_id: clientId,
        code: authCode,
	code_verifier: verifier,
    })
}).then(res => res.json())

app.get('/oauth_token', async (req, res) => {
    const url = req.protocol + '://' + req.get('host') + req.baseUrl;
    const verifier = req.session.codeVerifier;
    const lichessToken = await getLichessToken(req.query.code, verifier, url)

    res.json({ 'token-type': 'Bearer', token: lichessToken.access_token, message: 'Save your token somewhere' })
})

const deleteLichessToken = async (authCode) => await fetch('https://lichess.org/api/token', {
    method: 'DELETE',
    headers: {
        Authorization: `Bearer ${authCode}`,
        'Content-Type': 'application/json'
    }
}).then(res => {
    if (res.status == 204) {
        return 'Token deleted'
    }
})

app.get('/start', async (req, res) => {
    exec(`python C:\\Users\\Ivan\\Desktop\\chess-bot\\main.py ${req.code}`)
})

app.get('/stop', async (req, res) => {
    const lichessToken = await deleteLichessToken(req.query.code)
    res.json({message: lichessToken})
})

app.listen(port, () => { console.log(`Listening on ${port}`) })