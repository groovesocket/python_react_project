import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import PlayerList from './PlayerList';


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<PlayerList />} />
            </Routes>
        </Router>
    );
}


export default App;
