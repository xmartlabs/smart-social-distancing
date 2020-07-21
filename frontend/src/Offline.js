import React, { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import {
    Grid,
    Card,
    Radio,
    Button,
    TextField,
    Typography,
    CircularProgress,
} from "@material-ui/core";

const useStyle = makeStyles((theme) => ({
    bounding: {
        width: '100%',
        padding: theme.spacing(2, 2),
        margin: theme.spacing(2, 0),
        position: 'relative',
    },
    video_form: {
        width: '100%',
        padding: theme.spacing(2, 0),
    },
    video_option: {
        alignItems: 'center',
    },
    loading_background: {
        backgroundColor: 'white',
        opacity: '80%',
        position: 'absolute',
        width: '100%',
        height: '100%',
        zIndex: 2,
    },
    loading_spinner: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -20,
        marginLeft: -20,
        zIndex: 3,
    },
}));

export default function Offline() {
    const classes = useStyle();
    return (
        <Grid container spacing={3}>
            <Card variant="outlined" className={classes.bounding}>
                <VideoForm />
            </Card>
        </Grid>
    );
}

function VideoForm() {
    const classes = useStyle();
    const [fileSelected, setFileSelected] = useState(true);
    const [file, setFile] = useState(null);
    const [vidURL, setVidURL] = useState('');
    const [videoSent, setVideoSent] = useState(false);
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('huehuehue');

    const selectFile = () => {
        setFileSelected(true);
        setError(false);
    };
    const selectURL = () => {
        setFileSelected(false);
        setError(false);
    };

    const handleFileButton = (event) => {
        setFileSelected(true);
        setFile(event.target.files[0]);
    };
    const handleURLFieldKey = (event) => {
        if (event.key !== 'Enter') return;
        handleSubmit();
    };
    const handleURLFieldChange = (event) => {
        setVidURL(event.target.value);
    };
    
    const handleSubmit = () => {
        if (fileSelected) {
            if (!file) {
                setError(true);
                setErrorMessage('No file provided.');
                return;
            }
            //TODO: send file
        } else {
            if (!vidURL || vidURL === '') {
                setError(true);
                setErrorMessage('No URI provided.');
                return;
            }
            //TODO: send url
        }
        setError(false);
        setVideoSent(true);
    };

    useEffect(() => {
        if (!videoSent) return;
        let intervalId = setInterval(() => {setVideoSent(false)}, 3000);
        return () => clearInterval(intervalId);
    }, [videoSent])
    
    return (
        <Grid className={classes.video_form}>
            { videoSent && <div className={classes.loading_background} /> }
            { videoSent && <CircularProgress className={classes.loading_spinner} /> }
            <Typography variant="h6" color="textSecondary">
                Send us a video...
            </Typography>
            <Grid className={classes.video_form}>
                <Grid container className={classes.video_option}>
                    <Radio checked={fileSelected} onClick={selectFile} />
                    <Typography color="textPrimary">Local file:&nbsp;&nbsp;</Typography>
                    <input accept="video/*" id="file-select-button" type="file" onChange={handleFileButton} />
                </Grid>
                <Grid container className={classes.video_option}>
                    <Radio checked={!fileSelected} onClick={selectURL} style={{marginTop: 18}} />
                    <TextField
                        id="url"
                        label="http URI"
                        color="primary"
                        error={error && !fileSelected}
                        onClick={selectURL}
                        onKeyUp={handleURLFieldKey}
                        onChange={handleURLFieldChange}
                        style={{flexGrow: 1, marginRight: 16}}
                    />
                </Grid>
            </Grid>
            <Button type="button" variant="contained" color="primary" className={classes.button} onClick={handleSubmit}>
                Submit
            </Button>
            { error && <Typography variant="p">&nbsp;&nbsp;{errorMessage}</Typography>}
        </Grid>
    );
}