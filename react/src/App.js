const App = () => {
    const [pokemons, setPokemons] = React.useState([]);
    const [filteredPokemons, setFilteredPokemons] =React.useState([]);
    const onChangeHandler = (event) => {
        const comparedPokemons = pokemons.filter(
            pokemon => { return pokemon.name.includes(event.target.value)}
        )
        setFilteredPokemons(comparedPokemons);
    }
    React.useEffect(() => {
        fetch("https://pokeapi.co/api/v2/pokemon")
            .then(res => res.json())
            .then(json => {
                // 响应时，给每个result添加id
                json.results.map((result, index) =>{
                    result.id = index + 1;
                });
                setPokemons(json.results);
                setFilteredPokemons(json.results);
            });
    },[])
    

    return (
        <div>
            <h1>Pokemon</h1>
            <Input onChangeHandler = { onChangeHandler }/>
            <Lists pokemonLists= { filteredPokemons }/>
        </div> 
    )
}





/*
// 函数组件
class App extends React.Component{
    constructor() {
        console.log("构造器")
        super();
        this.state = {
            pokemons: [],
            filteredPokemons: [], // '皮卡丘','杰尼龟','小火龙'
            egg: 'chicken egg'
        };
    }

    componentDidMount(){
        console.log("组件已挂载")
        fetch("https://pokeapi.co/api/v2/pokemon")
            .then(res => res.json())
            .then(json => {
                // 响应时，给每个result添加id
                json.results.map((result, index) =>{
                    result.id = index + 1;
                });
                this.setState(
                    () => {
                        return {
                            pokemons: json.results,
                            filteredPokemons: json.results,
                        };
                    },
                    () => {
                        console.log(this.state);
                    }
                ); 
            });
    }


    onChangeHandler = (event) => {
        const comparedPokemons = this.state.pokemons.filter(
            pokemon => { return pokemon.name.includes(event.target.value)}
        )
        this.setState(
            () => {
                return { filteredPokemons: comparedPokemons };
            },
            () => {
                console.log(this.state.searching);
            }
        )
    }

    render(){
        console.log("渲染")
        return(
            <div>
                <h1>Pokemon</h1>
                <Input onChangeHandler = {this.onChangeHandler}/>
                <Lists pokemonLists= { this.state.filteredPokemons }/>
            </div>
        )
    };
}
*/