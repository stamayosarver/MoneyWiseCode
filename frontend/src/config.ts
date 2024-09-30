export default {
  auth0: {
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  },
  api: {
    baseUrl: import.meta.env.VITE_API_URL
  }
}