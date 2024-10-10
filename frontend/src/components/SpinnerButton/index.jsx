import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import { useState, useEffect } from "react";
function SpinnerButton({ clicked, onClick, callbackFunc}) {
    const [renders, setRenders] = useState(false);
    async function handleClick(eventKey) {
        setRenders(true)
        const taskID = await callbackFunc()
        getTaskResult(taskID)
      };
    async function getTaskResult(taskID){
        const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\task_result\\${taskID}`,
         {method: 'GET',});
        if (response.ok){
            setRenders(false)
        }
    }

  return (
    <>
      <Button variant="primary" onClick={handleClick}>
        {renders ? <Spinner
          as="span"
          animation="border"
          size="sm"
          role="status"
          aria-hidden="true"
        /> : <div></div>}
        <span>{renders ? 'Loading prices' : 'Update prices'}</span>
      </Button>
    </>
  );
}

export default SpinnerButton;