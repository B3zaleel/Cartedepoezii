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
          <a
            class="nav-link"
            href="#features-section"
            @click="ev => scrollToSect(ev, 'features-section')"
          >
            <span>Features</span>
          </a>
          <a
            class="nav-link"
            href="#about-section"
            @click="ev => scrollToSect(ev, 'about-section')"
          >
            <span>About</span>
          </a>
          <button class="nav-link" @click="visitSite">
            <LaunchIcon/>
            <span>Visit Site</span>
          </button>
        </nav>
      </div>

      <article class='app-about'>
        <div class="intro">
          <div class="preview">
            <img src="https://ik.imagekit.io/B3zaleel/cartedepoezii/info_about/Intro_YCGH1-rJY.png?tr=pr-true&ik-sdk-version=javascript-1.4.3&updatedAt=1647504057127"/>
          </div>

          <div class="info">
            <div>
              <span class="logo">
                <Logo/>
              </span>
              <h3 class="project-name">
                {{ name }}
              </h3>
              <span class="project-description">
                {{ description }}
              </span>
            </div>
          </div>
        </div>

        <div id="features-section">
          <div
            :class="{sect:true, feature: true, alt: (i + 1) % 2 === 0}"
            v-for="feature, i in features"
            :key="i"
          >
            <div class="preview">
              <img :src="feature.imgSrc"/>
            </div>

            <div class="summary">
              <div>
                <b class="title">{{ feature.title }}</b>
                <p class="description">{{ feature.description }}</p>
              </div>
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

        <div id="about-section" class="sect about dark-bg">
          <div>
            <p>
              {{ about }}
              <br/>
              <br/>
              <a
                class="cdp-btn text light"
                target="_blank"
                href="https://github.com/B3zaleel/Cartedepoezii"
              >
                <GitHubIcon/>
                <b>Join the team</b>
              </a>
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
import GitHubIcon from '@/assets/icons/social/GitHub.vue';
import TwitterIcon from '@/assets/icons/social/Twitter.vue';
import LinkedInIcon from '@/assets/icons/social/LinkedIn.vue';
import HelpCircleIcon from '@/assets/icons/HelpCircle.vue';

@Component({
  name: 'AboutView',
  methods: {
    scrollToSect(ev, sectId) {
      const el = document.getElementById(sectId);
      if (el) {
        const mainElement = el.parentElement?.parentElement;
        let headerHeight = 54;
        if (mainElement) {
          const header = mainElement.getElementsByClassName('header').item(0);
          if (header) {
            headerHeight = header.clientHeight;
          }
        }
        window.scrollTo({
          top: el.offsetTop - headerHeight,
          behavior: 'smooth',
        });
      }
      ev.preventDefault();
      ev.stopPropagation();
    },
    visitSite() {
      window.open('/', '_blank');
    },
  },
  components: {
    Logo,
    LaunchIcon,
    GitHubIcon,
    TwitterIcon,
    LinkedInIcon,
    HelpCircleIcon,
  },
})
export default class AboutView extends Vue {
  name = 'Cartedepoezii';

  description = 'Create and find poems you love.';

  about = [
    'Cartedepoezii was inspired by my love for poems and how',
    'poems are able to contain a condensed group of words that',
    'touch the soul.',
    'The name Cartedepoezii is of Norwegian origin and translates',
    'to “poem book”.',
    'Just as much as I like reading poems, I also enjoy poetizing',
    'during my free time.',
    'As such, I decided to create a platform where people could share',
    'one of the most beautiful pieces of literature (poems), which led',
    'to the birth of Cartedepoezii.',
  ].join(' ');

  features = [
    {
      title: 'Create poems.',
      description: 'Share your words of love, wisdom or humour with the world.',
      imgSrc: 'https://ik.imagekit.io/B3zaleel/cartedepoezii/info_about/Cartedepoezii_Feature_0_uc2Xrtwdz.webp?tr=pr-true&ik-sdk-version=javascript-1.4.3&updatedAt=1647449192804',
    },
    {
      title: 'React to poems.',
      description: 'Like and comment on poems that move you.',
      imgSrc: 'https://ik.imagekit.io/B3zaleel/cartedepoezii/info_about/Cartedepoezii_Feature_1_SjcJS0MnX.webp?tr=pr-true&ik-sdk-version=javascript-1.4.3&updatedAt=1647449128529',
    },
    {
      title: 'Connect with poets.',
      description: 'Follow poets you like and get their poems on your timeline.',
      imgSrc: 'https://ik.imagekit.io/B3zaleel/cartedepoezii/info_about/Cartedepoezii_Feature_2_8w0mjcycr.webp?tr=pr-true&ik-sdk-version=javascript-1.4.3&updatedAt=1647449162208',
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
}
</script>

<style lang="scss">
@use "@/assets/styles/views/info/about";
</style>
