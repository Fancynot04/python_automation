const Input = ({ onChangeHandler }) => {
    return (
        <input type="Search" onChange= { onChangeHandler } />
    );
};

/*class Input extends React.Component {
    render() { 
        const { onChangeHandler } = this.props;
        return (  
            <input type="Search" onChange= { onChangeHandler } />
        );
    }
}
*/