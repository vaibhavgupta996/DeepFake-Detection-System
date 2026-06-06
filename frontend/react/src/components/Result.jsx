function Result({result}){

if(!result){

return null;

}

return(

<div className="resultCard">

<h2>

{result.prediction}

</h2>

<h3>

Confidence:

{result.confidence}%

</h3>

</div>

)

}

export default Result;