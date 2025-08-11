import Router from './router/Router'
import { CookiesProvider } from 'react-cookie'
const App = () => {
  return (
    <div style={{ height: "100vh" }}>
      <CookiesProvider>
        <Router />
      </CookiesProvider>
    </div>
  )
}

export default App