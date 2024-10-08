import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PlayerModal from './PlayerModal';

function PlayerList() {
    const [players, setPlayers] = useState([]);
    const [selectedPlayer, setSelectedPlayer] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [description, setDescription] = useState("");

    useEffect(() => {
        axios.get("http://localhost:8000/api/players/")
            .then(response => setPlayers(response.data))
            .catch(error => console.error(error));
      }, []);

    const handleEdit = (player) => {
        const updatedHits = prompt(`Edit hits for ${player.player}:`, player.hits);
        if (updatedHits !== null && !isNaN(updatedHits)) {
            axios.post(`http://localhost:8000/api/players/${player.id}/update-stats`, {
                hits: parseInt(updatedHits),
            })
            .then(response => {
                setPlayers(players.map(p => p.id === player.id ? response.data : p));
            })
            .catch(error => console.error(error));
        } else {
            alert("Please enter a valid number for hits");
        }
    }

    const handlePlayerClick = async (player) => {
        setLoading(true);
        setSelectedPlayer(player);
        // Call the API to get the LLM-generated description
        try {
            const response = await axios.get(`http://localhost:8000/api/players/${player.id}`);
            setDescription(response.data.description);
        } catch (error) {
            console.error("Error fetching player description:", error);
            setDescription("Could not fetch description."); // Fallback message
        } finally {
            setLoading(false);
            setIsModalOpen(true);
        }
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedPlayer(null);
        setDescription(""); // Clear description on close
    };

    return (
        <div>
            <h1>Players List</h1>
            <ul style={{ listStyleType: 'none' }}>
                {players.map(player => (
                    <li key={player.id}>
                        <h3 style={{ cursor: 'pointer' }} onClick={() => handlePlayerClick(player)}>Player: {player.player}</h3>
                        <ul>
                            <li>Rank: {player.rank}</li>
                            <li>Hits: {player.hits}&nbsp;
                                <button onClick={() => handleEdit(player)}>Edit Hits</button>
                            </li>
                            <li>Year: {player.year}</li>
                            <li>Age: {player.age}</li>
                            <li>Bats: {player.bats}</li>
                        </ul>
                    </li>
                ))}
            </ul>
            {selectedPlayer && (
                <PlayerModal
                    isOpen={isModalOpen}
                    onRequestClose={closeModal}
                    player={selectedPlayer}
                    description={description}
                    loading={loading}
                    contentLabel="Player Details"
                />
            )}
        </div>
    );
}

export default PlayerList;
