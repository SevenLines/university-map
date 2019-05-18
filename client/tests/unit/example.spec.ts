import { expect } from 'chai'
import { shallowMount } from '@vue/test-utils'
import Floor from '@/components/Floor.vue'

describe('Floor.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(Floor, {
      propsData: { msg }
    })
    expect(wrapper.text()).to.include(msg)
  })
})
