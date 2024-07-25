/* React 组件需要以大写字母开头，并且通常是通过函数或类来定义的，这些函数或类返回 JSX。
注意组件类只能包含一个顶层标签
*/
var i = 1;
var myStyle = {
    fontSize: 100,
    color: '#234111'
};    
var arr = [
    <h1>stupid</h1>,
    <h2>idols</h2>
];
function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
  }
function HelloMessage(props) {
    return <h1>12345</h1>;
}
const element = <HelloMessage/>

ReactDOM.render(
<div>
<h1>{element}</h1>
<div>{arr}</div>
<h5>{arr}</h5>
<h1 style = {{fontSize:30}}>past</h1>
<Welcome name="World" />
</div>
,document.getElementById("root")
);


