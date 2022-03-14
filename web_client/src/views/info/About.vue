<template>
  <div class="content-container">
    <main>
      <div class="header">
        <div>
          <a href="/">
            <Logo/>
          </a>
        </div>

        <nav>
          <a class="nav-link" href="#features-section">
            <span>Features</span>
          </a>
          <a class="nav-link" href="#about-section">
            <span>About</span>
          </a>
          <button class="nav-link" @click="visitSite">
            <LaunchIcon/>
            <span>Visit Site</span>
          </button>

          <button class="nav-launch-btn">
            <DotsHexagonIcon/>
          </button>
        </nav>
      </div>

      <article class='app-about'>
        <div>
          <div>
            <img/>
          </div>

          <div>
            <Logo/>
            <h3>
              Cartedepoezii
            </h3>
            <span>
              Create and find the poems you love
            </span>
          </div>
        </div>

        <div id="features-section">
          <div
            class="sect feature"
            v-for="feature, i in features"
            :key="i"
          >
            <div>
              <img :src="feature.imgSrc"/>
            </div>

            <div>
              <b class="title">{{ feature.title }}</b>
              <p class="descr">{{ feature.description }}</p>
            </div>
          </div>
        </div>

        <div class="mini-sect">
          <h3>
            Join us today
          </h3>
          <a
            class="cdp-btn text"
            href="/sign-up"
            target="_blank"
          >
            Sign Up
          </a>
        </div>

        <div id="about-section" class="sect dark-bg">
          <div>
            <p>
              foo
            </p>
          </div>

          <div>
            <div
              class="contributor-card"
              v-for="contributor, i in contributors"
              :key="i"
            >
              <img :src="contributor.profilePhotoSrc"/>
              <b class="name">{{ contributor.name }}</b>
              <div class="socials">
                <a
                  v-for="social in contributor.socials"
                  :key="social.name"
                  :href="social.src"
                  target="_blank"
                >
                  <GitHubIcon v-if="social.name === 'GitHub'"/>
                  <TwitterIcon v-if="social.name === 'Twitter'"/>
                  <LinkedInIcon v-if="social.name === 'LinkedIn'"/>
                </a>
              </div>
            </div>
          </div>
        </div>

        <div class="footer">
          <div>
            <a href="/terms-of-service">Terms</a>
            <a href="/privacy-policy">Privacy</a>
          </div>

          <div>
            <a
              href="https://github.com/B3zaleel/Cartedepoezii/discussions/categories/q-a"
              target="_blank"
            >
              <HelpCircleIcon/>
              <span>Help</span>
            </a>
          </div>
        </div>
      </article>
    </main>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Logo from '@/assets/icons/Logo.vue';
import LaunchIcon from '@/assets/icons/Launch.vue';
import DotsHexagonIcon from '@/assets/icons/DotsHexagon.vue';
import GitHubIcon from '@/assets/icons/social/GitHub.vue';
import TwitterIcon from '@/assets/icons/social/Twitter.vue';
import LinkedInIcon from '@/assets/icons/social/LinkedIn.vue';
import HelpCircleIcon from '@/assets/icons/HelpCircle.vue';

@Component({
  name: 'AboutView',
  methods: {
    visitSite() {
      window.open('/', '_blank');
    },
  },
  components: {
    Logo,
    LaunchIcon,
    DotsHexagonIcon,
    GitHubIcon,
    TwitterIcon,
    LinkedInIcon,
    HelpCircleIcon,
  },
})
export default class AboutView extends Vue {
  userId! : string

  features = [
    {
      title: 'Post poems',
      description: '',
      imgSrc: '',
    },
    {
      title: 'Join the conversation',
      description: '',
      imgSrc: 'https://ik.imagekit.io/B3zaleel/cartedepoezii/info_about/Cartedepoezii_Feature_1_Ca9VLIwSy.webp?ik-sdk-version=javascript-1.4.3&updatedAt=1647283283281',
    },
    {
      title: 'Join the conversation',
      description: '',
      imgSrc: '',
    },
  ];

  contributors = [
    {
      name: 'Bezaleel Olakunori',
      profilePhotoSrc: 'https://avatars.githubusercontent.com/u/17376603?v=4',
      socials: [
        {
          name: 'GitHub',
          src: 'https://github.com/B3zaleel',
        },
        {
          name: 'Twitter',
          src: 'https://twitter.com/B3zaleel',
        },
        {
          name: 'LinkedIn',
          src: 'https://www.linkedin.com/in/bezaleel-olakunori-34335513a/',
        },
      ],
    },
  ];

  created(): void {
    this.userId = this.$route.params.id;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/views/info/about";
</style>
