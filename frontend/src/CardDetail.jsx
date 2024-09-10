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
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useParams } from 'react-router-dom';
import TableComponent from './components/Table'

function CardDetail() {
    const [isLoading, setIsLoading] = useState(true);
    const [requestData, setRequestData] = useState([])
    const [itemData, setItemData] = useState([])
    const { printingId } = useParams();

    useEffect(() => {
        async function getData() {
            const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\cards-info\\7hNLjcLRMQKf89KqdNzfw`)
            const requestData = await response.json()
            setRequestData(requestData)
            setIsLoading(false);
            console.log(requestData)
        }
        getData()
    }, [])

    return (
    <div>
<TableComponent requestData={requestData}/>
</div>

    );
}

export default CardDetail;