## react组件
> 两种类型，函数和类组件；注意组件类只能包含一个顶层标签
```js
//1.创建一个函数组件
function HelloMessage(props) {
    return <h1>Hello {props.name}!</h1>;
}
//2.hook且传参
const element = <HelloMessage name="john"/>;
//3.标签绑定dom元素
const root = ReactDOM.createRoot(document.getElementById("root"));
//4.组件渲染,只需找出父组件的render,就能看清整个的html结构
root.render(
    element
);
```
## 箭头函数 & this
> 箭头函数,更简短的函数且不绑定this（不更改this指向）
```js
// 基本格式，单一参数或单一表达式时，无需加外层()或 {}
(params) => {function statement}
```
> call,apply,bind
```js
function greet(greeting, punctuation) {  
    console.log(greeting + ', ' + this.name + punctuation);  
}  
const person = {  
    name: 'Alice'  
};  
// 使用call调用greet函数，并设置this为person对象  
greet.call(person, 'Hello', '!');  

// 使用apply调用greet函数，并设置this为person对象，参数作为数组传递
greet.apply(person, ['Hi', '.']);  

// 使用bind创建一个新函数，其this被绑定到person对象  
const boundGreet = greet.bind(person, 'Howdy');  
// 调用boundGreet，并传递剩余的参数  
console.log(boundGreet('!'));  
```

## Props
> props（属性）<br/>
> 1.将数据从父组件传入子组件的机制，对子组件只读；而定义state可以用来更新和修改数据<br/>
>   A.父组件使用state定义，子组件采用props获取<br/>
> 2.默认props：defaultProps设置组件的默认属性值<br/>
> 3.propsType：对props进行类型检查<br/>
> 4.解构props：简化代码<br/>
> 5.传递回调函数：父组件可将函数作为props传递给子组件<br/>
```js
// 解构props,这里{ name }代替props, 下面name代替this.props.name
const Greeting = ({ name }) => {
  return <h1>Hello, {name}!</h1>;
};
const App = () => {
  return <Greeting name="Alice" />;
};

// prop-types地址
<script src="https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/prop-types/15.8.1/prop-types.min.js" type="application/javascript"></script>
static propTypes = {
    title: PropTypes.string.isRequired, // 必须是字符串且必需
    age: PropTypes.number,              // 可选的数字
    isAdmin: PropTypes.bool,            // 可选的布尔值
    user: PropTypes.shape({             // 必须是具有特定形状的对象
      name: PropTypes.string,
      email: PropTypes.string
    }),
    options: PropTypes.oneOf(['option1', 'option2']), // 必须是特定值之一
};

// 利用函数回调实现子父组件属性同步更新？
```



## Q: 
    1.return {} 和 return () 区别？</br>
    2.() => {}是什么，对比优缺点 ? </br>
    3.const { onChangeHandler } = this.props ? </br>
    4.useState的解构赋值 ?
    5.useEffect ?
---
## schedule
```markdown
1. 组件和JSX
2. 插值和状态
    A. <html> { 插值表达式 } </html>
    B. 通过this.state保存数组类型，方便后续直接调用值来map循环
    C. 箭头表达式
        ----------------------------------
        var f = ([params]) => expression（单一）
        // 等价于以下写法
        var f = function([params]){
            return expression;
        }
        ----------------------------------
3. 挂载和状态设置
    A. componentDidMount() 先呈现轮廓再加载数据（组件挂载完毕后，再执行）
    B. setState中console.log会先执行，导致输出之前没更新的pokemons,（异步任务）
        但可以用其中两个参数来写，其中第二个必定在第一个之后执行
4. 生命周期
    A. 注意App类中各个函数的调用顺序和次数
5. 拆组件
6. 事件处理器
    A. onChangeHandler获取事件，得到输入值
    B. 调用类方法使用this
7. props
    A. props跨文件传输变量
8. 遍历
9. CSS
    A. 列表中插入获取图片,发现第一张图片永远不变
    B. 每次筛选后，index的序号都是从0-n,采用自定义id给每个result
10. useState
    A.把类组件 改为 函数组件
    B.this无法使用，使用useState进行解构赋值
11. useEffect

```