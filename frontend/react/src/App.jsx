import "./App.css";

import Upload from "./components/Upload";

function App(){

return(

<div className="app">

<div className="glass">

<h1>

Deepfake Detection AI

</h1>

<p>

Upload an image and detect whether it is Real or Fake

</p>

<Upload/>

</div>

</div>

)

}

export default App;