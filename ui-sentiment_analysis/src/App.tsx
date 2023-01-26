import { useState } from "react";
import "./App.css";

function App() {
  const [isLoading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [result, setResult] = useState({
    message: "",
    result: null
  });

  const handle = async () => {
    setLoading(true);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message.trim() }),
    };
    await fetch("http://127.0.0.1:5000/analyze", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setResult({
          message: data.message,
          result: data.result
        });
        setLoading(false);
        console.log(data)
      });
  };

  return (
    
    <>
      <div style = {{backgroundImage : `url("/background.jpg")`}}>
      <div className="app">
         <div className="card">
        
        <h4>Sentiment Analysis</h4>
        <form> 
         <div></div>
          <textarea className="myText"
            cols = {80}
            rows ={10}
            name="message"
            placeholder="Enter your comment"
            value={message}
            onChange={(e) => setMessage(e.target.value)
                          
            }
          />

         <button type="button" onClick={() => handle()} disabled={!message}>
            {isLoading ? <div className="loader" /> : "Analyze"}
          </button>
          {result.message && (
          <>
          <div>{result.result ? <div><img src="/up-thumb.gif" className="center" height={250}/></div> :
                                 <div><img src="/down-thumb.gif" className="center" height={250}/></div>}</div>
          </>
        )}
        </form>
      </div> 
      </div>
      </div>
    </>
  )
}

export default App;
