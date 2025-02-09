import {BrowserRouter, Routes, Route, Link, useNavigate, redirect} from "react-router-dom";


function App(){
  return <div>
    <BrowserRouter>
    <a href="/">ALLEN(THis will refetch)</a>  ||<Link to={"/login"}>Login</Link> | <Link to={"/signup"}>Signup</Link>
     <Routes>
       <Route path="/login" element={<LoginPage/>} />
       <Route path="/signup" element={<SignupPage/>} />
       <Route path='/' element={<LandingPage/>}/>
     </Routes>
     Common Footer || Bottom 
    </BrowserRouter>
    
  </div>
}
function LoginPage(){
    return <div>
      Login PAge
    </div>
}
function SignupPage(){
    return <div>
      Signup PAge
    </div>
}
function LandingPage(){
  return <div>
    Welcome
  </div>
}
export default App;