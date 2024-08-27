
// 清除除现在点击的元素之外所有class属性带active的元素，并给现在点击的元素添加active，
// 然后通过css中 .container>.panel active {flex:5} 和 transition属性实现动画过渡
const panelItems = document.querySelectorAll(".container > .panel")
panelItems.forEach(item => {
    item.addEventListener('click',() => {
        // 下面代码的初步理解：先遍历children中不是当前点击的元素放入[]列表中,然后再移除active
        [].filter.call(item.parentElement.children,el=>el !== item).forEach(el => el.classList.remove('active'));
        item.classList.add('active')
    });
});

 
// 方案二
// const panelItems = document.querySelectorAll(".container>.panel")
// panelItems.forEach(item => {
//     item.addEventListener('click',()=>{
//         panelItems.forEach(panel =>{
//             if(panel !== item){
//                 panel.classList.remove('active');
//             }
//         });
//         item.classList.add('active');
//     });
// });