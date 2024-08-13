
const Input = ({ onChangeHandler }) => {
    return (
        <div className="searchbar" >
            <span class="material-symbols-outlined">
                search
            </span>
            <input type="text" onChange={onChangeHandler} placeholder="Search for pokemon" />
        </div>
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