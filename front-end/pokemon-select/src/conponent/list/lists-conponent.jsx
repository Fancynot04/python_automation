const Lists = ({ pokemonLists }) => {
    const imgCSS = {
        border: "1px solid darkorange",
        borderRadius:"10px",
    };
    return (  
        <ul className="ul-container"> 
        {
            pokemonLists.map((pokemon) => {
                return (
                    <div className="ul-item" key= { pokemon.url }>
                        <li >{ pokemon.name }</li>
                        <img 
                            src={ `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id}.png` }
                            style={ imgCSS }
                        />
                    </div>
                    
                )
            })
                    
        }
        </ul>
    );
}

/*class Lists extends React.Component {
   
    render() {
        console.log("Lists组件渲染");
        const { pokemonLists } = this.props;   
        const imgCSS = {
            border: "1px solid darkorange",
            borderRadius:"10px",
        };
        return (  
            <ul className="ul-container"> 
            {
                pokemonLists.map((pokemon) => {
                    return (
                        <div key= { pokemon.url }>
                            <li >{ pokemon.name }</li>
                            <img 
                                src={ `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id}.png` }
                                style={ imgCSS }
                            />
                        </div>
                        
                    )
                })
                        
            }
            </ul>
        );
    }
}
*/