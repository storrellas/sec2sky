import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ReactMapboxGl, { Layer, Feature } from "react-mapbox-gl";
import GPX from 'gpx-for-runners';

const Map = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoic3RvcnJlbGxhcyIsImEiOiJjaWp6bHQ5Y3kwMDU4dmNtMHgzb2NhNmU5In0.M3jJSPh7KUT0QDSd7Bn3Rg"
});


const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: '100vh',
    overflow: 'auto',
  },
  chartContainer: {
    marginLeft: -22,
  },
  mapContainer: {
    height: 320,
    width: 220,
  },
  input: {
  display: 'none',
  }
});

class MapUnoceros extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      fitBounds: undefined,
      center: [-0.481747846041145, 51.3233379650232],
      zoom: [10],
      route : [
        [-0.481747846041145, 51.3233379650232],
        [-0.472757846041245, 51.3233379650232],
        [-0.463767846041345, 51.3233379650232],
        [-0.454777846041445, 51.3233379650232]
      ]
    };
  }

  handleOnReadEnd(){
    const content = fileReader.result;
    console.log(content)
  }

  handleInputFile(event){
    let fileReader = new FileReader()
    var obj = this;
    fileReader.onloadend = function(){
        const content = fileReader.result;
        const gpx = new GPX( content );
        obj.setState({
          route: gpx.trackpoints.map( trackpoint => [trackpoint.lon, trackpoint.lat])
        });
    }

    // Read file
    fileReader.readAsText(event.target.files[0])
  }

  render() {
    const { classes } = this.props;

    const position = []
    const { fitBounds, center, zoom, route } = this.state;

    const lineLayout = {
      'line-cap': 'round',
      'line-join': 'round'
    };

    const linePaint = {
      'line-color': '#4790E5',
      'line-width': 12
    };


    return (
        <main className={classes.content}>
          <div className={classes.appBarSpacer} />
          <Typography variant="h4" gutterBottom component="h2">
            GPX Reader
          </Typography>
          <Map
            style="mapbox://styles/mapbox/streets-v9"
            zoom={zoom}
            center={route[0]}
            containerStyle={{
              height: "400px",
              width: "800px"
            }}>
              <Layer type="line" layout={lineLayout} paint={linePaint}>
              <Feature coordinates={route} />
            </Layer>
          </Map>

          <input
            className={classes.input}
            id="contained-button-file"
            multiple
            type="file"
            onChange={this.handleInputFile.bind(this)}
          />
          <label htmlFor="contained-button-file">
            <Button variant="contained" component="span" className={classes.button}>
              Upload
            </Button>
          </label>
        </main>
    );
  }
}

export default withStyles(styles)(MapUnoceros);
