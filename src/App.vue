<template>
  <div id="app">
    <v-header :user="user"></v-header>
    <!-- <h1>Graduation Prject Template!</h1>
    <div id="nav">
     <router-link :to="{ name: 'home' }">Vue</router-link> |
     <router-link :to="{ name: 'messages' }">Django Rest</router-link>
    </div>
    <router-view/> -->
    <main>
              <!-- 左侧导航 -->
            <div class="main-left">
              <el-menu default-active="/home" class="el-menu-vertical-demo" :router="true">
                <el-menu-item index="/home" :class="{'isActive': active}">HOME</el-menu-item>
                <el-menu-item index="/messages" :class="{'isActive': !active}">Message</el-menu-item>
              </el-menu>
            </div>

              <!-- 右侧主内容区 -->
              <div  class="main-right" >
              <!-- 视图 -->
                <router-view class="view"></router-view>
              </div>
        </main>
  </div>
</template>

<script>
import header from './components/header.vue';
export default {
  data(){
    return {
      active: true,
      user: {}
    }
  },
  components: {
    'v-header': header
  },
  created: function(){
    this.$router.push('/home');
  },
  watch: {
     '$route': function (to, from) {
         if(to.path == '/home'){
             this.active = true ;
         }else if(to.path == '/messages'){
             this.active = false ;
         }
     }
  }
}
</script>


<style>
#app {
  /* font-family: 'Avenir', Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  font-family: "Helvetica Neue","PingFang SC",Arial,sans-serif;
}
#nap {
  color: red;
  font-size: 30px;
}
 /* 主内容区 */
main{display: -webkit-box;display: -ms-flexbox;display: flex;  min-height: 800px;  border: solid 40px #E9ECF1;  background-color: #FCFCFC;  }
main .main-left{text-align: center;-webkit-box-flex: 0;-ms-flex: 0 0 200px;flex: 0 0 200px;}
main .main-right{-webkit-box-flex:1;-ms-flex:1;flex:1; background-color: #fff; padding: 50px 70px; }
main .el-menu{background-color: transparent!important;}
/*  */
.router-link{display:inline-block;width:100%;height:100%;text-align:center;color:#475669;text-decoration: none; }
.is-active .router-link{color:#20a0ff; }
/* 单选框 */
  .el-form-item .el-radio+.el-radio {
    margin-left: 30px!important;
  }
  /* 路由切换动效 */
  .fade-enter-active, .fade-leave-active {
    transition: all .5s;
  }
  .fade-enter, .fade-leave-active {
    opacity: 0;
  }
  .list-enter-active, .list-leave-active {
    transition: all 1s;
  }
  .list-enter, .list-leave-active {
    opacity: 0;
    transform: translateY(30px);
  }
/* 导航栏菜单选中效果 */
  .isActive{color: #20a0ff!important;}
   #app main .aside .is-active{color: #475669;}
  /* 卡片 */
  .el-card{overflow: visible!important;}
</style>