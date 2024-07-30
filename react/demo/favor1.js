/*class Clock extends React.Component {
    constructor(props) {
        console.log("构造器");
        super(props);
        this.state = {date: new Date()};
    }
   
    componentDidMount() {
        console.log("挂载");
      this.timerID = setInterval(
        () => this.tick(),
        1000
      );
    }
   
    componentWillUnmount() {
        console.log("卸载");
      clearInterval(this.timerID);
    }
   
    tick() {
        console.log("tick");
      this.setState({
        date: new Date()
      });
    }
   
    render() {
        console.log("渲染");
      return (
        <div>
          <h1>Hello, world!</h1>
          <h2>现在是 {this.state.date.toLocaleTimeString()}.</h2>
        </div>
      );
    }
  }

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(<Clock />) */

class CptBody extends React.Component{
    constructor(){
        console.log("constructor");
        super();
        this.state = {username : 1}; //可以传json等很多格式（这个是初始化赋值）
    }
    //click事件函数
    changeAge(){
        console.log("click事件函数");
        this.setState({username:1+this.state.username})
    }
    //change事件函数
    changeUsername(event){
        console.log("change事件函数");
        this.setState({username:parseInt(event.target.value)})
    }
    render(){
        console.log("parent 渲染");
       return(
            <div>
                <h1>下面的操作有惊喜</h1>
                <p>{this.state.username}</p>
                <input type="button" value="点击改变username" onClick={()=>this.changeAge()}/>
                <BodyChild changeUsername={this.changeUsername.bind(this)} getname={this.state.username}/>
            </div>
        )
    }
}


class BodyChild extends React.Component{
    render(){
        console.log("child 渲染");
        return(
            <div>
                <p>子页面输入：<input type='text' value={this.props.getname} onChange={this.props.changeUsername} /></p>

            </div>
        )
    }
}
ReactDOM.render(
    <CptBody  />,
    document.getElementById('root')
);