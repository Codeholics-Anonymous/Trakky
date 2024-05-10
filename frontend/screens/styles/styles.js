import { StatusBar, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    scrollContainer: {
        flex: 1,
    },
    container: {
      flexGrow: 1,
      paddingTop: StatusBar.currentHeight,
      alignItems: 'center',
      backgroundColor: '#565656',
    },
    box: {
      borderWidth: 8,
      borderColor: '#878787',
      borderRadius: 25,
      alignItems: 'center',
      backgroundColor: '#d3d3d3',
      height: '10%',
      width: '90%',
      marginTop: '4%',
      justifyContent: 'center',
  
      elevation: 8
    },
    headerContainer: {
      backgroundColor: '#878787',
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'flex-start',  // Aligns children to the start; used with absolute positioning of center content
      width: '100%',
      height: '7.5%',
      paddingHorizontal: 15, // Adjusts padding for breathing space on edges
      elevation: 18
    },
    options: {
      width: 35,
      height: 35,
      marginLeft: 'auto',  // This pushes the options icon to the right
    },
    centerContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      position: 'absolute',
      left: 0,
      right: 0,
      justifyContent: 'center',
    },
    logo: {
      width: 50,
      height: 50,
      marginRight: 10,
    },
    header: {
      fontSize: 20,
      color: 'white',
      fontWeight: 'bold'
    },
    circleContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between', // This will space out the elements within the container
      width: '100%', // Take up full width to allow outer spacing
      paddingHorizontal: '8%', // Adjust this value to increase space from the screen edges
      marginBottom: 0,
      marginTop: 20
    },
    date: {
      fontSize: 15,
      color: '#333333',
      marginTop: 2,
      marginBottom: 2,
      marginLeft: 10
    },
    navText: {
      fontSize: 80,
      transform: [{ scaleY: 1.5}],
      color: '#d3d3d3',
      fontFamily: 'Poppins-Regular',
    },
    caloriesCurrent: {
      fontSize: 20,
      color: 'white',
      fontWeight: 'bold'
    },
    caloriesGoal: {
      fontSize: 16,
      color: '#eeeeee',
      fontWeight: 'bold'
    },
    boxText: {
      fontSize: 24,
      color: '#333333',
      fontWeight: 'bold',
      justifyContent: 'center',  // Centers content vertically in the container
      alignItems: 'center',       // Centers content horizontally in the container
    },
    dateContainer: {
        backgroundColor: '#878787',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',  // Aligns children to the start; used with absolute positioning of center content
        paddingHorizontal: 15, // Adjusts padding for breathing space on edges
        elevation: 14,

        borderWidth: 4,
        borderColor: '#878787',
        borderRadius: 17,
        alignItems: 'center',
        backgroundColor: '#d3d3d3',
        height: '4.5%',
        width: '50%',
        marginTop: '3%'
    },
    calendar: {
        width: 22,
        height: 22,
        marginLeft: 10,
    }
  });

  export default styles;