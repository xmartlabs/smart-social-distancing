import axios from 'axios';
import React, { useEffect, useState, useLayoutEffect } from "react";
import {makeStyles} from "@material-ui/core/styles";
import {
    Card,
    Table,
    TableBody,
    TableCell,
    TableRow,
    Grid,
    Typography,
    IconButton,
    CircularProgress
} from "@material-ui/core";
import RefreshIcon from '@material-ui/icons/Refresh';
import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly, { dash } from 'plotly.js-cartesian-dist'
import {mergeDeepLeft} from "ramda";
import ContainerDimensions from "react-container-dimensions";
import {Player, BigPlayButton} from 'video-react';
import HLSSource from './components/HLSSource';
import h337 from 'heatmap.js';
import "video-react/dist/video-react.css";

const Plot = createPlotlyComponent(Plotly);

const useStyle = makeStyles((theme) => ({
    fullWidth: {
        width: '100%',
    },
    withPadding: {
        padding: theme.spacing(1, 2),
    },
    marginTopLeft: {
        marginTop: theme.spacing(1),
        marginLeft: theme.spacing(2),
    },
    refreshButton: {
        position: 'absolute',
        top: theme.spacing(1),
        left: theme.spacing(1),
        zIndex: 10,
    }
}));

function CameraFeed({cameras}) {
    const classes = useStyle();
    const [time, _] = useState(new Date().toISOString()); // time is appended to live urls to prevent caching
    console.log(cameras ? `${cameras[0].streams[0].src}?${time}` : '');
    return (
        <Card className={classes.withPadding} variant="outlined">
            <Typography variant="h6" color="textSecondary">
                Camera Feed
            </Typography>
            {cameras ? (
                <Player muted={true} autoPlay={true}>
                    <HLSSource isVideoChild src={`${cameras[0].streams[0].src}?${time}`}/>
                    <BigPlayButton position="center" />
                </Player>
            ) : <CircularProgress/>}
        </Card>
    );
}

function StatsSimpleRow({label, value}) {
    return <TableRow>
        <TableCell component="th" scope="row">{label}</TableCell>
        <TableCell>{value}</TableCell>
    </TableRow>
}

function Status() {
    const classes = useStyle();
    const [time, _] = useState(new Date().toISOString());

    return (
        <Card variant="outlined">
            <Typography variant="h6" color="textSecondary" className={classes.marginTopLeft}>
                Status
            </Typography>
            <Table size="small">
                <TableBody>
                    <StatsSimpleRow label="Environment Score" value={12}/>
                    <StatsSimpleRow label="Time" value={time}/>
                    <StatsSimpleRow label="Camera IP" value="127.0.0.1"/>
                </TableBody>
            </Table>
        </Card>
    )
}

function BirdsView({cameras}) {
    const classes = useStyle();
    const [time, _] = useState(new Date().toISOString()); // time is appended to live urls to prevent caching

    return (
        <Card variant="outlined" className={classes.withPadding}>
            <Typography variant="h6" color="textSecondary">
                Bird's View
            </Typography>
            {cameras ? (
                <Player muted={true} autoPlay={true} fluid={false}>
                    <HLSSource isVideoChild src={`${cameras[0].streams[1].src}?${time}`}/>
                    <BigPlayButton position="center" />
                </Player>
            ) : <CircularProgress/>}
        </Card>
    );
}

function Charts({cameras}) {
    const classes = useStyle();
    const [data, setData] = useState(undefined)
    const [heatmapDetections, setHeatmapDetections] = useState(undefined);

    function update() {
        const headers = {'Cache-Control': 'no-store'};
        if (!cameras) {
            return
        }
        const url = `${cameras[0]['storage_host']}/static/data/${cameras[0]['id']}/objects_log/${new Date().toISOString().slice(0, 10)}.csv`;
        axios.get(url, {headers}).then(response => {
            const records = Plotly.d3.csv.parse(response.data);
            const x1 = [], y1 = [], y2 = [], env_score = [];
            let detections = [];
            let lastTimestamp = '';
            records.forEach(function (element) {
                // Graphs
                x1.push(element['Timestamp']);
                y1.push(element['DetectedObjects']);
                y2.push(element['ViolatingObjects']);
                env_score.push((element['EnvironmentScore']));

                // Heatmap
                lastTimestamp = element['Timestamp'];
                JSON.parse(element['Detections'].replaceAll('\'', '\"')).forEach((detection) => {
                    detections.push(detection);
                });
            });
            setData({x1, y1, y2, env_score});
            setHeatmapDetections(detections);
        })
        // Plotly.d3.csv(, (records) => {
        // })
    }

    useEffect(() => {
        let intervalId = setInterval(update, 15000);  // refresh chart every 15 seconds
        return () => clearInterval(intervalId);
    }, [cameras]);
    useEffect(update, [cameras]);

    const [envScoreFigure, setEnvScoreFigure] = useState(undefined)

    useEffect(() => {
        if (!data) return;
        setEnvScoreFigure({
            data: [{
                x: data.x1,
                y: data.env_score,
                fill: 'tozeroy',
                type: 'scatter',
                name: 'Environment Score'
            }],
            layout: {
                title: 'Plotting log data Physical Distancing - Environment Score',
                height: 300,
            }
        })
    }, [data]);

    const [pedestriansFigure, setPedestriansFigure] = useState(undefined)

    useEffect(() => {
        if (!data) return;
        let detected_pedestrians = {
            x: data.x1,
            y: data.y1,
            fill: 'tozeroy',
            type: 'scatter',
            name: 'Detected Pedestrians'
        };
        let detected_violating_pedestrians = {
            x: data.x1,
            y: data.y2,
            fill: 'tozeroy',
            type: 'scatter',
            name: 'Detected Pedestrians In Unsafe Area'
        };

        setPedestriansFigure({
            data: [detected_pedestrians, detected_violating_pedestrians],
            onInitialized: setPedestriansFigure,
            onUpdated: setPedestriansFigure,
            layout: {
                title: 'Plotting log data Physical Distancing',
                height: 300,
            }
        })
    }, [data]);

    return (
        <Card variant="outlined" className={classes.withPadding}>
            {data ? (
                <ContainerDimensions>
                    {({width}) => (
                        <React.Fragment>
                            <IconButton className={classes.refreshButton} onClick={update}>
                                <RefreshIcon/>
                            </IconButton>
                            <Plot {...mergeDeepLeft(pedestriansFigure, {layout: {width: width - 20}})}/>
                            <Plot {...mergeDeepLeft(envScoreFigure, {layout: {width: width - 20}})}/>
                            <Heatmap width={width} aspectRatio={3/4} detections={heatmapDetections} />
                        </React.Fragment>
                    )}
                </ContainerDimensions>
            ) : ''}
        </Card>
    );
}

function Heatmap(props) {
    const [heatmap, updateHeatmap] = useState(undefined);
    const [dimensions, updateDimensions] = useState({ width: undefined, height: undefined });

    const updateHeatmapData = (detections) => {
        if (!heatmap || !dimensions.width || !dimensions.height) return;
        const heatmapResolutionX = 150;
        const heatmapResolutionY = Math.floor(heatmapResolutionX * props.aspectRatio);
        let max = 0;
        const grid = Array(heatmapResolutionX).fill()
            .map(() => Array(heatmapResolutionY).fill(0));
        detections.forEach((detection) => {
            for (const value of [detection.bbox]) if (value < 0 || value > 1) return;
            const x = Math.floor((detection.bbox[0] + detection.bbox[2]) * heatmapResolutionX / 2);
            const y = Math.floor((detection.bbox[1] + detection.bbox[3]) * heatmapResolutionY / 2);
            grid[x][y] += 1 / (1 + grid[x][y]);
            if (grid[x][y] > max) max = grid[x][y]; 
        });

        const points = [];
        for (let i = 0; i < heatmapResolutionX; i += 1) {
            for (let j = 0; j < heatmapResolutionY; j += 1) {
                if (grid[i][j] > 0) {
                    points.push({
                        x: i * dimensions.width / heatmapResolutionX,
                        y: j * dimensions.height / heatmapResolutionY,
                        value: grid[i][j],
                    });
                }
            }
        }

        console.log(points);
        updateHeatmap(heatmap.setData({
            max,
            data: points,
        }));
    };

    useEffect(() => {
        if (!heatmap) {
            const heatmapContainer = document.querySelector('.heatmapjs');
            setSize(heatmapContainer);
        }
    }, []);

    
    useEffect(() => {
        if (!props.detections) return;
        updateHeatmapData(props.detections);
    }, [props.detections]);
    
    useEffect(() => {
        setSize(document.querySelector('.heatmapjs'), props.width);
    },[props.width]);
    
    const setSize = (container) => {
        const width = props.width - 35;
        const aspectRatio = props.aspectRatio;
        updateDimensions({
            width: Math.floor(width),
            height: Math.floor(width * aspectRatio),
        });
        container.style.width = `${Math.floor(width)}px`
        container.style.height = `${Math.floor(width * aspectRatio)}px`
        if (heatmap) heatmap._renderer.canvas.remove();
        updateHeatmap(undefined);
        updateHeatmap(h337.create({
            container,
        }));
    };

    return (
        <div>
            <Typography variant="h6" color="textSecondary">
                Heatmap
            </Typography>
            <div className="heatmapjs" style={{height:'1000px',width:'100%'}}>
                <img /*src={ TODO: Get frame from video to show as background }*/ style={{height:'100%',width:'100%'}}/>
            </div>
        </div>
    );
}

export default function Live() {
    const classes = useStyle();
    const [now, _] = useState(new Date().getTime())
    const [cameras, setCameras] = useState(undefined);
    useEffect(() => {
        axios.get('/api/cameras').then(response => setCameras(response.data))
    }, []);
    return (
        <Grid container spacing={3}>
            <Grid item xs={12} md={7}>
                <CameraFeed cameras={cameras}/>
            </Grid>
            <Grid item container xs={12} md={5} spacing={3}>
                {process.env.NODE_ENV === 'development' /* IN_PROGRESS */ ? (
                    <Grid item xs={12}>
                        <Status/>
                    </Grid>
                ) : null}
                <Grid item xs={12}>
                    <BirdsView cameras={cameras} />
                </Grid>
            </Grid>
            <Grid item xs={12}>
                <Charts cameras={cameras}/>
            </Grid>
        </Grid>
    );
}