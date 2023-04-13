class APIOnlineChecker {
    constructor(driver) {
      this.driver = driver;
    }
  
    async isOnline() {
      try {
        await this.driver.get('api-status/');
        return true;
      } catch (error) {
        return false;
      }
    }
  }
  
  export default APIOnlineChecker;
  