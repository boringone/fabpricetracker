import React from "react";
import { useState, useEffect } from "react";
import "./App.css";
import CardExample from "./components/Card";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import Container from 'react-bootstrap/Container';
import BasicExample from './components/Search';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Pagination from '@mui/material/Pagination';
import { useParams } from 'react-router-dom';
import { useNavigate } from "react-router-dom"
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
    const navigate = useNavigate()
    const { pageNumb } = useParams();
    const [isLoading, setIsLoading] = useState(true);
    const [requestData, setRequestData] = useState([])
    const [setData, setSetData] = useState([]);
    const [currentSet, setCurrentSet] = useState('');
    const [itemData, setItemData] = useState([])
    const [currentPage, setCurrentPage] = useState(parseInt(pageNumb) ? parseInt(pageNumb) : 1)
    function createItemObject(requestData) {
        return  Object.assign({}, ...requestData.results.map(item => ({[item.unique_id]: item.cardprinting_set})))
    }
    function handleChange(event){
        navigate(`/${event.target.innerText}`)
        setCurrentPage(parseInt(event.target.innerText))
    }
    useEffect(() => {
        async function getSetData() {
            if (!setData.length){
                const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\set-info\\`)
                const setData = await response.json()
                setSetData(setData)
            }
        }
        async function getData() {
            const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\card-info\\?page=${currentPage}&set_id=${currentSet}`)
            const requestData = await response.json()
            setRequestData(requestData)
            const urlParams = new URL(requestData.next);
            const itemArray = createItemObject(requestData)
            console.log(requestData)
            console.log(itemArray)
            setItemData(itemArray)
            setIsLoading(false);
        }
        getData()
        getSetData()
    }, [currentPage])

    return (
    <div>
      <Container>
        <BasicExample setData={setData}/>
        <Row xxl={2} xl={2} lg={2} md={1} sm={1}>
            {isLoading?
            (<div>Loading…</div>)
            :
            (requestData.results.map((item) => <Col><CardExample key={item.unique_id} requestData={item} itemData={itemData[item.unique_id]} /></Col>))}
        </Row>
    <Pagination count={40} page={currentPage} onChange={handleChange} />
    </Container>
</div>
    );
}

export default App;