import { expect } from 'chai'
import { shallowMount } from '@vue/test-utils'
import Building from '@/components/Floor.vue'

describe('Building.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(Building, {
      propsData: { msg }
    })
    expect(wrapper.text()).to.include(msg)
  })
})
