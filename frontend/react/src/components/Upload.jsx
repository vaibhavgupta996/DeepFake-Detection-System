import { useState } from "react";

import Result from "./Result";

function Upload() {

const [file, setFile] = useState(null);

const [loading, setLoading] = useState(false);

const [result, setResult] = useState(null);

const submit = async () => {

try {

if (!file) {

alert("Please Select Image");

return;

}

setLoading(true);

setResult(null);

const formData = new FormData();

formData.append(

"image",

file

);

console.log("Sending Request...");

const response = await fetch(

"http://127.0.0.1:5000/predict",

{

method: "POST",

body: formData

}

);

console.log("Status:", response.status);

const data = await response.json();

console.log(data);

if(data.error){

alert(data.error);

return;

}

setResult(data);

}

catch(err){

console.log(err);

alert("Connection Error");

}

finally{

setLoading(false);

}

};

return (

<div>

<div className="uploadBox">

<input

type="file"

accept="image/*"

onChange={(e)=>{

setFile(

e.target.files[0]

)

}}

/>

</div>

<button

className="btn"

onClick={submit}

disabled={loading}

>

{

loading

?

"Predicting..."

:

"Detect"

}

</button>

<Result result={result}/>

</div>

);

}

export default Upload;