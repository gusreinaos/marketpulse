//Author: Michael Larsson

import styles from './media-post-component.module.scss';
import React, { useEffect, useState } from 'react';
import { Col, Row } from 'react-bootstrap';
import userIcon from '../../../assets/icons8-user-50.png'

interface MediaPostProp {
    data: {
        message: string,
        user: string,
        time: string
    }
}


const MediaPostComponent: React.FC<MediaPostProp> = ({data}) => {
    const [showFullMessage, setShowFullMessage] = useState(false);

    const toggleShowFullMessage = () => {
        setShowFullMessage(!showFullMessage);
    };

    return (
        <Col>
            <div className={styles.media}>
                <p className={styles.mediaTitle}>
                    <img src={userIcon} alt='userIcon'></img>
                    <span className={styles.usernameText}>{data.user}</span>
                </p>
                <p className={styles.mediaText}>
                    {showFullMessage ? data.message : `${data.message.slice(0, 100)}...`}
                    {data.message.length > 120 && (
                        <button onClick={toggleShowFullMessage} className={styles.readMoreButton}>
                            {showFullMessage ? 'Read Less' : 'Read More'}
                        </button>
                    )}</p>
                <p className={styles.mediaTime}>{data.time}</p>
            </div>
        </Col>
    )
}


export default MediaPostComponent;