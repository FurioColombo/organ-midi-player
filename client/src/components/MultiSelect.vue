<template>
  <div class="multi-select-container">
    <label>{{ label }}</label>
    <div class="select-wrapper" @click="toggleDropdown">
      <div class="custom-select">
        {{ selectedOptions.length > 0 ? selectedOptions.join(', ') : 'Select channels' }}
      </div>
      <div v-if="showDropdown" >
        <ul class="dropdown-list">
          <li v-for="option in options" :key="option.value" @click="toggleOption(option.value)">
            <input type="checkbox" :value="option.value" v-model="selectedOptions">
            {{ option.label }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false,
      selectedOptions: [],
    };
  },

  props: {
    label: String,
    options: Array,
  },

  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
      // Emit an event with the updated selected options
      this.$emit('update:selectedOptions', this.selectedOptions);
    },

    toggleOption(optionValue) {
      const index = this.selectedOptions.indexOf(optionValue);
      if (index === -1) {
        this.selectedOptions.push(optionValue);
      } else {
        this.selectedOptions.splice(index, 1);
      }
      // Emit an event with the updated selected options
      this.$emit('update:selectedOptions', this.selectedOptions);
    },
  },
};
</script>

<style scoped>
.multi-select-container {
  display: inline-block;
  margin-right: 10px;
}

.select-wrapper {
  position: relative;
  display: inline-block;
}

.custom-select {
  padding: 8px;
  border: 1px solid #3498db;
  border-radius: 5px;
  font-size: 14px;
  background-color: #3498db;
  color: #fff;
  cursor: pointer;
  width: 150px;
  text-align: left;
}

.dropdown-list {
  list-style: none;
  padding: 0;
  margin-left: 0;
  margin-right: 0;
  margin-top: 0;
  position: absolute;
  top: 100%;
  left: 5px;
  right: 5px;
  background-color: #fff;
  border: 1px solid #3498db;
  border-top: 0;
  border-radius: 0; /* Remove rounded borders */
  box-sizing: border-box; /* Include padding and border in the width */
  text-align: left;
}

.dropdown-list li {
  padding: 8px;
  cursor: pointer;
}

.dropdown-list li:hover {
  background-color: #3498db;
  color: #fff;
}
</style>
