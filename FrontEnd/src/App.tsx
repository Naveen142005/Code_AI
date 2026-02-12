import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './components/home';
import Chat from "./components/chat";

function App() {    
  return (
    <BrowserRouter>
        <Routes>
            <Route path="/" element= {<Home/>}></Route>
            <Route path="/chat" element= {<Chat/>}></Route>
        </Routes>
    </BrowserRouter>
  )
}
export default App;