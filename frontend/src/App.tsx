import React from 'react';

import './App.css';
import { Container } from 'react-bootstrap'
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom'
import Urlcounts from './Urlcounts'

export const App = () => {
    return (
        <Router basename={'/'}>
            <Container>
                <Routes>
                    <Route path='/' element={<Urlcounts/>} />
                </Routes>
            </Container>
        </Router>
    )
}
