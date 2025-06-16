<template>
  <div class="map-list">
    <h1>選擇一張地圖</h1>
    <div class="grid">
      <div 
        v-for="map in maps" 
        :key="map.name" 
        class="map-box" 
        @click="goToMap(map.name)">
        <div class="box"></div>
        <p>{{ map.name }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapList',
  data() {
    return {
      maps: [
        { name: 'Dust2' },
        { name: 'Mirage' },
        { name: 'Nuke' },
        { name: 'Inferno' },
        { name: 'Anibus' },
        { name: 'Train' },
        { name: 'Ancient' }
      ]
    }
  },
  methods: {
    goToMap(mapName) {
      this.$router.push(`/map/${mapName}`)
    }
  }
}
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 40px;
  justify-items: center;
}
.map-box {
  text-align: center;
  cursor: pointer;
}
.box {
  width: 120px;
  height: 120px;
  border: 4px solid black;
  margin-bottom: 8px;
}
</style>
