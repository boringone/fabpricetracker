import React from "react";
import { useState, useEffect } from "react";
import "./App.css";
import CardExample from "./components/Card";
import NavbarExample from "./components/Navbar";
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
import { useSearchParams } from "react-router-dom";
import useAuthFetch from "./hooks/authApiFetch"

function App() {
    const navigate = useNavigate()
    let [searchParams, setSearchParams] = useSearchParams();
    const [isLoading, setIsLoading] = useState(true);
    const [itemData, setItemData] = useState([])

//  Data states
    const [setData, setSetData] = useState([]);
    const [typeData, setTypeData] = useState([]);
    const [requestData, setRequestData] = useState([])


    function createFilterObject() {
        const filterObject = Object.assign({}, ...['set', 'type', 'name'].map(item => ({[item]: searchParams.get(item) ? searchParams.get(item) : ''})))
        filterObject.pageNumb = parseInt(searchParams.get('pageNumb')) ? parseInt(searchParams.get('pageNumb')) : 1
        return filterObject
    }
    function createItemObject(requestData) {
        return  Object.assign({}, ...requestData.results.map(item => ({[item.unique_id]: item.cardprinting_set})))
    }

    function handlePageChange(event){
        const filterData = createFilterObject()
        filterData.pageNumb = parseInt(event.target.innerText)
        setSearchParams(filterData);
    }

    useEffect(() => {
        async function getSetData() {
            if (!setData.length){
                const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\set-info\\`)
                const setData = await response.json()
                setSetData(setData)
            }
        }
        async function getTypeData() {
            if (!typeData.length){
                const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\types-info\\`)
                if (!response.ok){
                    return
                }
                const typeData = await response.json()
                setTypeData(typeData[0].unnested_types)
            }
        }

        async function getData() {
            const filterData = createFilterObject()
            const response = await fetch(`${import.meta.env.VITE_SERVER_URL}\\card-info\\?page=${filterData.pageNumb}&set_id=${filterData.set}&name=${filterData.name}&type=${filterData.type}`)
            const requestData = await response.json()
            setRequestData(requestData)
            const itemArray = createItemObject(requestData)
            console.log(requestData)
            console.log(itemArray)
            setItemData(itemArray)
            setIsLoading(false);
        }
        getData()
        getSetData()
        getTypeData()
    }, [searchParams])

    return (
    <div>
        <NavbarExample loggedIn={true}/>
      <Container>
        {isLoading? (<div></div>) : (<BasicExample setData={setData} typeData={typeData} onSubmit={setSearchParams}/>)}
        <Row xxl={2} xl={2} lg={2} md={1} sm={1}>
            {isLoading?
            (<div>Loading…</div>)
            :
            (requestData.results.map((item) => <Col><CardExample key={item.unique_id} requestData={item} itemData={itemData[item.unique_id]} /></Col>))}
        </Row>
    {isLoading? (<div></div>) : <Pagination count={requestData.total_pages} page={createFilterObject().pageNumb} onChange={handlePageChange} />}
    </Container>
</div>
    );
}

export default App;