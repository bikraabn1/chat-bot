import axios from 'axios'

axios.defaults.withCredentials = true

export const useAuth = () => {
    const handleLoginWithGoogle = () => {
        const rootUrl = "https://accounts.google.com/o/oauth2/v2/auth"

        const options = {
            redirect_uri: `${import.meta.env.VITE_BACKEND_URL}/auth/callback`,
            client_id: import.meta.env.VITE_CLIENT_ID,
            access_type: "offline",
            response_type: "code",
            prompt: "consent",
            scope: [
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email"
            ].join(" ")
        }

        const qs = new URLSearchParams(options)
        window.location.href = `${rootUrl}?${qs.toString()}`
    }

    const handleLoginWithJWT = async (username, password) => {
        try {
            await axios.post(
                `${import.meta.env.VITE_BACKEND_URL}/auth/login-jwt`,
                {
                    username: username,
                    password: password
                }, {
                withCredentials: true
            }
            )
            return true
        } catch (err) {
            return false
        }
    }



    return { handleLoginWithGoogle, handleLoginWithJWT }
}