import MainLayout from './layout/main-layout'
import ChatPage from './pages/chat-page/ChatPage'

const App = () => {
  return (
    <div style={{height: "100vh"}}>
      <MainLayout>
        <ChatPage/>
      </MainLayout>
    </div>
  )
}

export default App