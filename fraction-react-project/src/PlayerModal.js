import React from 'react';
import Modal from 'react-modal';
Modal.setAppElement('body');

const PlayerModal = ({ isOpen, onRequestClose, player, description, loading }) => {
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            contentLabel="Player Description"
        >
            <h2>{player.player}</h2>
            {loading ? (
                <p>Loading description...</p>
            ) : (
                <p>{description}</p>
            )}
            <button onClick={onRequestClose}>Close</button>
        </Modal>
    );
};

export default PlayerModal;