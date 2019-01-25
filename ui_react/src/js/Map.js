import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import NotificationsIcon from '@material-ui/icons/Notifications';
import ReactMapboxGl, { Layer, Feature } from "react-mapbox-gl";
import GPX from 'gpx-for-runners';

import { mainListItems, secondaryListItems } from './listItems';
import SimpleLineChart from './SimpleLineChart';
import SimpleTable from './SimpleTable';
import NavBar from './NavBar';
import SideBar from './SideBar';

const Mapbox = ReactMapboxGl({
  accessToken: "pk.eyJ1Ijoic3RvcnJlbGxhcyIsImEiOiJjaWp6bHQ5Y3kwMDU4dmNtMHgzb2NhNmU5In0.M3jJSPh7KUT0QDSd7Bn3Rg"
});


const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 9,
    },
  },
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
  tableContainer: {
    height: 320,
  },
  chartContainer: {
    marginLeft: -22,
  },
  mapContainer: {
    height: 320,
    width: 220,
  },
  input: {
    display: 'none'
  },
  h5: {
    marginBottom: theme.spacing.unit * 2,
  },
});

class Map extends React.Component {
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
      <div className={classes.root}>
        <CssBaseline />
        <NavBar />
        <SideBar />
        <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Typography variant="h4" gutterBottom component="h2">
          GPX Reader
        </Typography>
        <Mapbox
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
        </Mapbox>

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
      </div>
    );
  }
}

Map.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Map);
